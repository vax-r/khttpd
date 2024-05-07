from bcc import BPF
code = """
#include <uapi/linux/ptrace.h>

BPF_HASH(start, u64);

int kprobe__my_thread_run(struct pt_regs *ctx)
{
    u64 ts, key = 0;
	ts = bpf_ktime_get_ns();
	start.update(&key, &ts);
    return 0;
}

int kretprobe__my_thread_run(struct pt_regs *ctx)
{
    u64 key = 0;
    u64 *ts = start.lookup(&key);
	u64 end_ts = bpf_ktime_get_ns();
	if (ts != NULL) {
        u64 delta = end_ts - *ts;
		bpf_trace_printk("%llu\\n", delta);
		start.delete(&key);
    }
	
	start.update(&key, &end_ts);
    return 0;
}
"""

b = BPF(text = code)

with open('kthread_run_cost.txt', 'w') as f:
    i = 0
    while True:
        try:
            (task, pid, cpu, flags, ts, msg) = b.trace_fields()
            f.write(str(i))
            f.write(' ')
            f.write(msg.decode("UTF-8"))
            f.write('\n')
            i += 1
        except ValueError:
            continue
