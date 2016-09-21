	.file	"notfibonacci.c"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4,,15
	.globl	trickfun
	.type	trickfun, @function
trickfun:
.LFB23:
	.cfi_startproc
	testl	%edi, %edi
	je	.L31
	leaq	16(%rdx), %r8
	leaq	16(%rsi), %r10
	cmpq	%r8, %rsi
	leal	-1(%rdi), %eax
	setnb	%r11b
	cmpq	%rdx, %r10
	setbe	%r8b
	orl	%r11d, %r8d
	cmpl	$8, %edi
	seta	%r11b
	testb	%r11b, %r8b
	je	.L3
	leaq	16(%rcx), %r8
	cmpq	%r8, %rsi
	setnb	%r11b
	cmpq	%rcx, %r10
	setbe	%r8b
	orb	%r8b, %r11b
	je	.L3
	movl	%eax, %r9d
	movq	%rdx, %rax
	pushq	%r12
	.cfi_def_cfa_offset 16
	.cfi_offset 12, -16
	andl	$15, %eax
	pushq	%rbp
	.cfi_def_cfa_offset 24
	.cfi_offset 6, -24
	shrq	$2, %rax
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
	negq	%rax
	movl	%eax, %r8d
	andl	$3, %r8d
	cmpl	%edi, %r8d
	movl	%r8d, %eax
	cmova	%edi, %eax
	testl	%eax, %eax
	je	.L13
	movss	(%rdx), %xmm0
	leaq	4(%rsi), %r10
	cmpl	$1, %eax
	addss	(%rcx), %xmm0
	leaq	4(%rdx), %r11
	leaq	4(%rcx), %rbx
	leal	-2(%rdi), %r9d
	movss	%xmm0, (%rsi)
	je	.L4
	movss	4(%rdx), %xmm0
	leaq	8(%rsi), %r10
	cmpl	$3, %eax
	addss	4(%rcx), %xmm0
	leaq	8(%rdx), %r11
	leaq	8(%rcx), %rbx
	leal	-3(%rdi), %r9d
	movss	%xmm0, 4(%rsi)
	jne	.L4
	movss	8(%rdx), %xmm0
	leaq	12(%rsi), %r10
	addss	8(%rcx), %xmm0
	leaq	12(%rdx), %r11
	leaq	12(%rcx), %rbx
	leal	-4(%rdi), %r9d
	movss	%xmm0, 8(%rsi)
.L4:
	subl	%eax, %edi
	movl	%eax, %eax
	xorl	%r12d, %r12d
	leal	-4(%rdi), %r8d
	salq	$2, %rax
	shrl	$2, %r8d
	addq	%rax, %rdx
	addq	%rax, %rcx
	addl	$1, %r8d
	addq	%rsi, %rax
	xorl	%esi, %esi
	leal	0(,%r8,4), %ebp
.L6:
	pxor	%xmm0, %xmm0
	movlps	(%rcx,%rsi), %xmm0
	addl	$1, %r12d
	movhps	8(%rcx,%rsi), %xmm0
	addps	(%rdx,%rsi), %xmm0
	movlps	%xmm0, (%rax,%rsi)
	movhps	%xmm0, 8(%rax,%rsi)
	addq	$16, %rsi
	cmpl	%r8d, %r12d
	jb	.L6
	movl	%ebp, %eax
	subl	%ebp, %r9d
	salq	$2, %rax
	addq	%rax, %r10
	addq	%rax, %r11
	addq	%rax, %rbx
	cmpl	%ebp, %edi
	je	.L1
	movss	(%rbx), %xmm0
	testl	%r9d, %r9d
	addss	(%r11), %xmm0
	movss	%xmm0, (%r10)
	je	.L1
	movss	4(%r11), %xmm0
	cmpl	$1, %r9d
	addss	4(%rbx), %xmm0
	movss	%xmm0, 4(%r10)
	je	.L1
	movss	8(%r11), %xmm0
	addss	8(%rbx), %xmm0
	movss	%xmm0, 8(%r10)
.L1:
	popq	%rbx
	.cfi_restore 3
	.cfi_def_cfa_offset 24
	popq	%rbp
	.cfi_restore 6
	.cfi_def_cfa_offset 16
	popq	%r12
	.cfi_restore 12
	.cfi_def_cfa_offset 8
.L31:
	ret
	.p2align 4,,10
	.p2align 3
.L13:
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
	.cfi_offset 6, -24
	.cfi_offset 12, -16
	movq	%rcx, %rbx
	movq	%rdx, %r11
	movq	%rsi, %r10
	jmp	.L4
	.p2align 4,,10
	.p2align 3
.L3:
	.cfi_def_cfa_offset 8
	.cfi_restore 3
	.cfi_restore 6
	.cfi_restore 12
	movl	%eax, %edi
	xorl	%eax, %eax
	addq	$1, %rdi
	.p2align 4,,10
	.p2align 3
.L11:
	movss	(%rdx,%rax,4), %xmm0
	addss	(%rcx,%rax,4), %xmm0
	movss	%xmm0, (%rsi,%rax,4)
	addq	$1, %rax
	cmpq	%rdi, %rax
	jne	.L11
	ret
	.cfi_endproc
.LFE23:
	.size	trickfun, .-trickfun
	.section	.text.unlikely
.LCOLDE0:
	.text
.LHOTE0:
	.section	.text.unlikely
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4,,15
	.globl	restrictfun
	.type	restrictfun, @function
restrictfun:
.LFB24:
	.cfi_startproc
	testl	%edi, %edi
	je	.L61
	movq	%rdx, %rax
	pushq	%r13
	.cfi_def_cfa_offset 16
	.cfi_offset 13, -16
	andl	$15, %eax
	pushq	%r12
	.cfi_def_cfa_offset 24
	.cfi_offset 12, -24
	shrq	$2, %rax
	pushq	%rbp
	.cfi_def_cfa_offset 32
	.cfi_offset 6, -32
	leal	-1(%rdi), %ebp
	negq	%rax
	pushq	%rbx
	.cfi_def_cfa_offset 40
	.cfi_offset 3, -40
	andl	$3, %eax
	cmpl	%edi, %eax
	cmova	%edi, %eax
	cmpl	$4, %edi
	ja	.L63
	movl	%edi, %eax
.L36:
	movss	(%rdx), %xmm0
	leaq	4(%rsi), %r9
	cmpl	$1, %eax
	addss	(%rcx), %xmm0
	leaq	4(%rdx), %r11
	leaq	4(%rcx), %r10
	leal	-2(%rdi), %r8d
	movss	%xmm0, (%rsi)
	je	.L38
	movss	4(%rdx), %xmm0
	leaq	8(%rsi), %r9
	cmpl	$2, %eax
	addss	4(%rcx), %xmm0
	leaq	8(%rdx), %r11
	leaq	8(%rcx), %r10
	leal	-3(%rdi), %r8d
	movss	%xmm0, 4(%rsi)
	je	.L38
	movss	8(%rdx), %xmm0
	leaq	12(%rsi), %r9
	cmpl	$4, %eax
	addss	8(%rcx), %xmm0
	leaq	12(%rdx), %r11
	leaq	12(%rcx), %r10
	leal	-4(%rdi), %r8d
	movss	%xmm0, 8(%rsi)
	jne	.L38
	movss	12(%rdx), %xmm0
	leaq	16(%rsi), %r9
	addss	12(%rcx), %xmm0
	leaq	16(%rdx), %r11
	leaq	16(%rcx), %r10
	leal	-5(%rdi), %r8d
	movss	%xmm0, 12(%rsi)
.L38:
	cmpl	%eax, %edi
	je	.L34
.L37:
	subl	%eax, %edi
	subl	%eax, %ebp
	movl	%eax, %r13d
	leal	-4(%rdi), %ebx
	shrl	$2, %ebx
	addl	$1, %ebx
	cmpl	$2, %ebp
	leal	0(,%rbx,4), %r12d
	jbe	.L40
	leaq	0(,%r13,4), %rax
	xorl	%ebp, %ebp
	addq	%rax, %rdx
	addq	%rax, %rcx
	addq	%rax, %rsi
	xorl	%eax, %eax
.L41:
	pxor	%xmm0, %xmm0
	movlps	(%rcx,%rax), %xmm0
	addl	$1, %ebp
	movhps	8(%rcx,%rax), %xmm0
	addps	(%rdx,%rax), %xmm0
	movlps	%xmm0, (%rsi,%rax)
	movhps	%xmm0, 8(%rsi,%rax)
	addq	$16, %rax
	cmpl	%ebp, %ebx
	ja	.L41
	movl	%r12d, %eax
	subl	%r12d, %r8d
	salq	$2, %rax
	addq	%rax, %r9
	addq	%rax, %r11
	addq	%rax, %r10
	cmpl	%r12d, %edi
	je	.L34
.L40:
	movss	(%r10), %xmm0
	testl	%r8d, %r8d
	addss	(%r11), %xmm0
	movss	%xmm0, (%r9)
	je	.L34
	movss	4(%r11), %xmm0
	cmpl	$1, %r8d
	addss	4(%r10), %xmm0
	movss	%xmm0, 4(%r9)
	je	.L34
	movss	8(%r11), %xmm0
	addss	8(%r10), %xmm0
	movss	%xmm0, 8(%r9)
.L34:
	popq	%rbx
	.cfi_restore 3
	.cfi_def_cfa_offset 32
	popq	%rbp
	.cfi_restore 6
	.cfi_def_cfa_offset 24
	popq	%r12
	.cfi_restore 12
	.cfi_def_cfa_offset 16
	popq	%r13
	.cfi_restore 13
	.cfi_def_cfa_offset 8
.L61:
	ret
	.p2align 4,,10
	.p2align 3
.L63:
	.cfi_def_cfa_offset 40
	.cfi_offset 3, -40
	.cfi_offset 6, -32
	.cfi_offset 12, -24
	.cfi_offset 13, -16
	testl	%eax, %eax
	jne	.L36
	movl	%ebp, %r8d
	movq	%rcx, %r10
	movq	%rdx, %r11
	movq	%rsi, %r9
	jmp	.L37
	.cfi_endproc
.LFE24:
	.size	restrictfun, .-restrictfun
	.section	.text.unlikely
.LCOLDE1:
	.text
.LHOTE1:
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC2:
	.string	"\n---used as intended---"
.LC6:
	.string	"%d: %f\n"
.LC7:
	.string	"\n---without restrict---"
.LC9:
	.string	"\n---with restrict---"
	.section	.text.unlikely
.LCOLDB10:
	.section	.text.startup,"ax",@progbits
.LHOTB10:
	.p2align 4,,15
	.globl	main
	.type	main, @function
main:
.LFB25:
	.cfi_startproc
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	movl	$.LC2, %edi
	xorl	%ebx, %ebx
	subq	$192, %rsp
	.cfi_def_cfa_offset 208
	movq	%fs:40, %rax
	movq	%rax, 184(%rsp)
	xorl	%eax, %eax
	call	puts
	movaps	.LC5(%rip), %xmm0
	movl	$0x40000000, 112(%rsp)
	movl	$0x40400000, 176(%rsp)
	movaps	%xmm0, (%rsp)
	movaps	%xmm0, 16(%rsp)
	movaps	%xmm0, 32(%rsp)
	movss	.LC3(%rip), %xmm0
	addss	.LC4(%rip), %xmm0
	movl	$0x40000000, 116(%rsp)
	movl	$0x40400000, 180(%rsp)
	movss	%xmm0, 48(%rsp)
	movss	%xmm0, 52(%rsp)
	.p2align 4,,10
	.p2align 3
.L65:
	movl	%ebx, %edx
	pxor	%xmm0, %xmm0
	movl	$.LC6, %esi
	cvtss2sd	(%rsp,%rbx,4), %xmm0
	movl	$1, %edi
	movl	$1, %eax
	addq	$1, %rbx
	call	__printf_chk
	cmpq	$14, %rbx
	jne	.L65
	movl	$.LC7, %edi
	xorl	%ebx, %ebx
	call	puts
	movl	$0x3f800000, (%rsp)
	movss	.LC3(%rip), %xmm1
	addss	.LC8(%rip), %xmm1
	movl	$0x40000000, 4(%rsp)
	movss	.LC3(%rip), %xmm0
	movl	$0x44188000, 52(%rsp)
	addss	%xmm1, %xmm0
	movss	%xmm1, 8(%rsp)
	addss	%xmm0, %xmm1
	movss	%xmm0, 12(%rsp)
	addss	%xmm1, %xmm0
	movss	%xmm1, 16(%rsp)
	addss	%xmm0, %xmm1
	movss	%xmm0, 20(%rsp)
	addss	%xmm1, %xmm0
	movss	%xmm1, 24(%rsp)
	addss	%xmm0, %xmm1
	movss	%xmm0, 28(%rsp)
	addss	%xmm1, %xmm0
	movss	%xmm1, 32(%rsp)
	addss	%xmm0, %xmm1
	movss	%xmm0, 36(%rsp)
	addss	%xmm1, %xmm0
	movss	%xmm1, 40(%rsp)
	movss	%xmm0, 44(%rsp)
	addss	%xmm1, %xmm0
	movss	%xmm0, 48(%rsp)
	.p2align 4,,10
	.p2align 3
.L66:
	movl	%ebx, %edx
	pxor	%xmm0, %xmm0
	movl	$.LC6, %esi
	cvtss2sd	(%rsp,%rbx,4), %xmm0
	movl	$1, %edi
	movl	$1, %eax
	addq	$1, %rbx
	call	__printf_chk
	cmpq	$14, %rbx
	jne	.L66
	movl	$.LC9, %edi
	xorl	%ebx, %ebx
	call	puts
	pxor	%xmm0, %xmm0
	movl	$0x40000000, 4(%rsp)
	movlps	4(%rsp), %xmm0
	movl	$0x3f800000, (%rsp)
	movhps	12(%rsp), %xmm0
	addps	(%rsp), %xmm0
	movhps	%xmm0, 16(%rsp)
	movlps	%xmm0, 8(%rsp)
	pxor	%xmm0, %xmm0
	movlps	20(%rsp), %xmm0
	movhps	28(%rsp), %xmm0
	addps	16(%rsp), %xmm0
	movhps	%xmm0, 32(%rsp)
	movlps	%xmm0, 24(%rsp)
	pxor	%xmm0, %xmm0
	movlps	36(%rsp), %xmm0
	movhps	44(%rsp), %xmm0
	addps	32(%rsp), %xmm0
	movlps	%xmm0, 40(%rsp)
	movhps	%xmm0, 48(%rsp)
	.p2align 4,,10
	.p2align 3
.L67:
	movl	%ebx, %edx
	pxor	%xmm0, %xmm0
	movl	$.LC6, %esi
	cvtss2sd	(%rsp,%rbx,4), %xmm0
	movl	$1, %edi
	movl	$1, %eax
	addq	$1, %rbx
	call	__printf_chk
	cmpq	$14, %rbx
	jne	.L67
	xorl	%eax, %eax
	movq	184(%rsp), %rcx
	xorq	%fs:40, %rcx
	jne	.L73
	addq	$192, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 16
	popq	%rbx
	.cfi_def_cfa_offset 8
	ret
.L73:
	.cfi_restore_state
	call	__stack_chk_fail
	.cfi_endproc
.LFE25:
	.size	main, .-main
	.section	.text.unlikely
.LCOLDE10:
	.section	.text.startup
.LHOTE10:
	.section	.rodata.cst4,"aM",@progbits,4
	.align 4
.LC3:
	.long	1073741824
	.align 4
.LC4:
	.long	1077936128
	.section	.rodata.cst16,"aM",@progbits,16
	.align 16
.LC5:
	.long	1084227584
	.long	1084227584
	.long	1084227584
	.long	1084227584
	.section	.rodata.cst4
	.align 4
.LC8:
	.long	1065353216
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.2) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
