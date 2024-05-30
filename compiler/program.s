	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 14, 0
	.globl	_factorial                      ## -- Begin function factorial
	.p2align	4, 0x90
_factorial:                             ## @factorial
	.cfi_startproc
## %bb.0:
	pushq	%rbx
	.cfi_def_cfa_offset 16
	subq	$16, %rsp
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -16
	movl	$0, 8(%rsp)
	movl	%edi, 12(%rsp)
	testl	%edi, %edi
	je	LBB0_1
## %bb.2:                               ## %if_1.else
	movl	12(%rsp), %ebx
	leal	-1(%rbx), %edi
	callq	_factorial
	imull	%ebx, %eax
	movl	%eax, 8(%rsp)
	jmp	LBB0_3
LBB0_1:                                 ## %if_1.then
	movl	$1, 8(%rsp)
LBB0_3:                                 ## %if_1.end
	movl	8(%rsp), %eax
	addq	$16, %rsp
	popq	%rbx
	retq
	.cfi_endproc
                                        ## -- End function
	.globl	_main                           ## -- Begin function main
	.p2align	4, 0x90
_main:                                  ## @main
	.cfi_startproc
## %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$5, 4(%rsp)
	movl	$5, %edi
	callq	_factorial
	movl	%eax, (%rsp)
	movl	%eax, %edi
	callq	_print_int
	popq	%rax
	retq
	.cfi_endproc
                                        ## -- End function
.subsections_via_symbols
