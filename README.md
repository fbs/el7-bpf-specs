# ebpf-specs

**Status: Stable**

A collection of rpm specs to build eBPF related tools on Centos 7. All tools are
available as static binaries to remove the potential runtime dependencies on the
used GCC and LLVM/Clang versions

Available tools:

- [bcc](https://github.com/iovisor/bcc)
- [bpftrace](https://github.com/iovisor/bpftrace)
- [bpftool](https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/tree/tools/bpf/bpftool)

## Repository

Repository available at https://repos.baslab.org/bpftools/

Install:

```
curl https://repos.baslab.org/bpftools.repo --output /etc/yum.repos.d/bpftools.repo
```

# bpftrace

Tools:

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


Tools marked with an :white_check_mark: have been "tested", the tool runs and
the output appears valid, but no indepth testing has been done. :x: indicate
tools that are known to be broken and those marked with :question: have not been
tested at all.

Unsupported builtins:

- cgroupid

# BCC

Tools:

| Tools          | Status             |
|----------------|--------------------|
| argdist        | :question:         |
| bashreadline   | :white_check_mark: |
| biolatency     | :white_check_mark: |
| biosnoop       | :white_check_mark: |
| biotop         | :white_check_mark: |
| bitesize       | :question:         |
| bpflist        | :white_check_mark: |
| btrfsdist      | :question:         |
| btrfsslower    | :question:         |
| cachestat      | :white_check_mark: |
| cachetop       | :white_check_mark: |
| capable        | :question:         |
| cobjnew        | :question:         |
| cpudist        | :question:         |
| cpuunclaimed   | :question:         |
| criticalstat   | :question:         |
| dbslower       | :question:         |
| dbstat         | :question:         |
| dcsnoop        | :question:         |
| dcstat         | :question:         |
| deadlock       | :question:         |
| drsnoop        | :question:         |
| execsnoop      | :question:         |
| exitsnoop      | :question:         |
| ext4dist       | :question:         |
| ext4slower     | :question:         |
| filelife       | :question:         |
| fileslower     | :question:         |
| filetop        | :question:         |
| funccount      | :question:         |
| funclatency    | :question:         |
| funcslower     | :question:         |
| gethostlatency | :question:         |
| hardirqs       | :question:         |
| inject         | :question:         |
| javacalls      | :question:         |
| javaflow       | :question:         |
| javagc         | :question:         |
| javaobjnew     | :question:         |
| javastat       | :question:         |
| javathreads    | :question:         |
| killsnoop      | :question:         |
| llcstat        | :question:         |
| mdflush        | :question:         |
| memleak        | :question:         |
| mountsnoop     | :question:         |
| mysqld_qslower | :question:         |
| nfsdist        | :question:         |
| nfsslower      | :question:         |
| nodegc         | :question:         |
| nodestat       | :question:         |
| offcputime     | :question:         |
| offwaketime    | :question:         |
| oomkill        | :question:         |
| opensnoop      | :question:         |
| perlcalls      | :question:         |
| perlflow       | :question:         |
| perlstat       | :question:         |
| phpcalls       | :question:         |
| phpflow        | :question:         |
| phpstat        | :question:         |
| pidpersec      | :question:         |
| profile        | :question:         |
| pythoncalls    | :question:         |
| pythonflow     | :question:         |
| pythongc       | :question:         |
| pythonstat     | :question:         |
| reset-trace    | :question:         |
| rubycalls      | :question:         |
| rubyflow       | :question:         |
| rubygc         | :question:         |
| rubyobjnew     | :question:         |
| rubystat       | :question:         |
| runqlat        | :question:         |
| runqlen        | :question:         |
| runqslower     | :question:         |
| shmsnoop       | :question:         |
| slabratetop    | :question:         |
| sofdsnoop      | :question:         |
| softirqs       | :question:         |
| solisten       | :question:         |
| sslsniff       | :question:         |
| stackcount     | :question:         |
| statsnoop      | :question:         |
| syncsnoop      | :question:         |
| syscount       | :question:         |
| tclcalls       | :question:         |
| tclflow        | :question:         |
| tclobjnew      | :question:         |
| tclstat        | :question:         |
| tcpaccept      | :question:         |
| tcpconnect     | :white_check_mark: |
| tcpconnlat     | :white_check_mark:         |
| tcpdrop        | :white_check_mark:         |
| tcplife        | :question:         |
| tcpretrans     | :question:         |
| tcpstates      | :question:         |
| tcpsubnet      | :question:         |
| tcptop         | :question:         |
| tcptracer      | :question:         |
| tplist         | :question:         |
| trace          | :question:         |
| ttysnoop       | :white_check_mark: |
| vfscount       | :question:         |
| vfsstat        | :question:         |
| wakeuptime     | :question:         |
| xfsdist        | :question:         |
| xfsslower      | :question:         |
| zfsdist        | :question:         |
| zfsslower      | :question:         |


Tools marked with an :white_check_mark: have been "tested", the tool runs and
the output appears valid, but no indepth testing has been done. :x: indicate
tools that are known to be broken and those marked with :question: have not been
tested at all.

# Building

**Some builds are done with GCC from `devtoolset-7` from software collections
to provide a modern GCC*

`build-all.sh` builds all tools in a docker container and exports the RPMs at
the end. It starts of by building LLVM and Clang and creating a "builder" image
with that, using that image it will build the other RPMs.
As building LLVM & Clang takes a while the process can be sped up by reusing an
earlier built image using the `--image-tag` flag

Alternatively you can build the spec files manually:

The first step is to build `llvm-clang` to provide a somewhat modern LLVM &
Clang, and to provide static libs. Make sure you install the generated rpms
before you go on the next step.

After that bcc and then bpftrace can be built, bpftrace depends on bcc so make
sure you install the version you just compiled. Although it also seems to work
with the version currently shipped with CentOS 7.

bpftool is stand alone.
