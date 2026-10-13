/*
 * Runner nhỏ dùng để chạy bài nộp với giới hạn tài nguyên và đo chính xác thời gian CPU / bộ nhớ.
 * (Nếu fork trực tiếp từ server Python, bộ nhớ đo được bị cộng cả phần RSS của tiến trình Python.)
 *
 * Cách dùng: runner <cpu_ms> <mem_mb> <wall_ms> <stdin> <stdout> <stderr> <cmd> [args...]
 * In ra:     <exit_code> <signal> <cpu_ms> <maxrss_kb> <killed_by_wall>
 */
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

static long long now_ms(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (long long)ts.tv_sec * 1000 + ts.tv_nsec / 1000000;
}

int main(int argc, char **argv) {
    if (argc < 8) {
        fprintf(stderr, "usage: runner cpu_ms mem_mb wall_ms in out err cmd...\n");
        return 2;
    }
    long cpu_ms = atol(argv[1]), mem_mb = atol(argv[2]), wall_ms = atol(argv[3]);
    pid_t pid = fork();
    if (pid < 0) { perror("fork"); return 2; }
    if (pid == 0) {
        setsid();
        int fi = open(argv[4], O_RDONLY), fo = open(argv[5], O_WRONLY | O_CREAT | O_TRUNC, 0644),
            fe = open(argv[6], O_WRONLY | O_CREAT | O_TRUNC, 0644);
        if (fi < 0 || fo < 0 || fe < 0) _exit(126);
        dup2(fi, 0); dup2(fo, 1); dup2(fe, 2);
        close(fi); close(fo); close(fe);
        struct rlimit r;
        r.rlim_cur = cpu_ms / 1000 + 1; r.rlim_max = r.rlim_cur + 1; setrlimit(RLIMIT_CPU, &r);
        r.rlim_cur = r.rlim_max = (rlim_t)mem_mb << 20; setrlimit(RLIMIT_AS, &r); setrlimit(RLIMIT_STACK, &r);
        r.rlim_cur = r.rlim_max = 64 << 20; setrlimit(RLIMIT_FSIZE, &r);
        r.rlim_cur = r.rlim_max = 0; setrlimit(RLIMIT_CORE, &r);
        execvp(argv[7], argv + 7);
        _exit(127);
    }
    long long start = now_ms();
    int status = 0, killed = 0;
    struct rusage ru;
    for (;;) {
        pid_t w = wait4(pid, &status, WNOHANG, &ru);
        if (w == pid) break;
        if (w < 0 && errno != EINTR) { perror("wait4"); return 2; }
        if (now_ms() - start > wall_ms) {
            kill(-pid, SIGKILL); kill(pid, SIGKILL);
            killed = 1;
            wait4(pid, &status, 0, &ru);
            break;
        }
        struct timespec ts = {0, 1000000};
        nanosleep(&ts, NULL);
    }
    long long cpu = (long long)ru.ru_utime.tv_sec * 1000 + ru.ru_utime.tv_usec / 1000 +
                    (long long)ru.ru_stime.tv_sec * 1000 + ru.ru_stime.tv_usec / 1000;
    int code = WIFEXITED(status) ? WEXITSTATUS(status) : -1;
    int sig = WIFSIGNALED(status) ? WTERMSIG(status) : 0;
    printf("%d %d %lld %ld %d\n", code, sig, cpu, ru.ru_maxrss, killed);
    return 0;
}
