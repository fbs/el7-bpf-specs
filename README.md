# ebpf-specs

**Satus: Usable but still WIP. Might rename some stuff and some tools need
patching still**

A collection of rpm specs to build eBPF related tools on Centos 7. All tools are
available as static binaries to remove the potential runtime dependencies on the
used GCC and LLVM/Clang versions

Available tools:

- [bcc](https://github.com/iovisor/bcc)
- [bpftrace](https://github.com/iovisor/bpftrace)
- [bpftool](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/tools/bpf/bpftool)

# BCC

Currently unpatched and barely tested. Some of the tools won't works

# bpftrace

| Tool              | Status                       |
|-------------------|------------------------------|
| bashreadline.bt   | :white_check_mark:           |
| biolatency.bt     | :white_check_mark:           |
| biosnoop.bt       | :white_check_mark:           |
| bitesize.bt       | :x:                          |
| capable.bt        | :white_check_mark:           |
| cpuwalk.bt        | :white_check_mark:           |
| dcsnoop.bt        | :white_check_mark:           |
| execsnoop.bt      | :white_check_mark: (patched) |
| gethostlatency.bt | :white_check_mark: (patched) |
| killsnoop.bt      | :white_check_mark:           |
| loads.bt          | :white_check_mark:           |
| mdflush.bt        | :x:                          |
| oomkill.bt        | :x:                          |
| opensnoop.bt      | :white_check_mark:           |
| pidpersec.bt      | :white_check_mark:           |
| runqlat.bt        | :white_check_mark:           |
| runqlen.bt        | :white_check_mark:           |
| statsnoop.bt      | :x:                          |
| syncsnoop.bt      | :white_check_mark:           |
| syscount.bt       | :white_check_mark:           |
| tcpaccept.bt      | :white_check_mark:           |
| tcpconnect.bt     | :white_check_mark:           |
| tcpdrop.bt        | :white_check_mark:           |
| tcpretrans.bt     | :white_check_mark:           |
| vfscount.bt       | :white_check_mark:           |
| vfsstat.bt        | :white_check_mark:           |
| writeback.bt      | :white_check_mark:           |
| xfsdist.bt        | :white_check_mark:           |
| ext4dist.bt       | :new:                        |

# Building

**Some builds are done with GCC from `devtoolset-7` from software collections
provide a modern GCC**

The first step is to build `llvm-clang` to provide a somewhat modern LLVM &
Clang, and to provide static libs.

After that bcc and then bpftrace can be built.

bpftool is stand alone.
