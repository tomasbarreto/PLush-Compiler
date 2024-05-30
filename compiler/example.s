	.section	__TEXT,__text,regular,pure_instructions
	.build_version macos, 14, 0
	.globl	_calcFibonaciNumber             ## -- Begin function calcFibonaciNumber
	.p2align	4, 0x90
_calcFibonaciNumber:                    ## @calcFibonaciNumber
	.cfi_startproc
## %bb.0:
	pushq	%rbx
	.cfi_def_cfa_offset 16
	subq	$16, %rsp
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -16
	movl	$0, 12(%rsp)
	movl	%edi, 8(%rsp)
	movl	$0, 4(%rsp)
	cmpl	$1, %edi
	jg	LBB0_2
## %bb.1:                               ## %if_1.then
	movl	8(%rsp), %eax
	jmp	LBB0_3
LBB0_2:                                 ## %if_1.else
	movl	8(%rsp), %edi
	decl	%edi
	callq	_calcFibonaciNumber
	movl	%eax, %ebx
	movl	8(%rsp), %edi
	addl	$-2, %edi
	callq	_calcFibonaciNumber
	addl	%ebx, %eax
LBB0_3:                                 ## %if_1.end
	movl	%eax, 4(%rsp)
	movl	4(%rsp), %eax
	movl	%eax, 12(%rsp)
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
	subq	$24, %rsp
	.cfi_def_cfa_offset 32
	movq	%rdi, 16(%rsp)
	movl	_prt_1(%rip), %edi
	callq	_calcFibonaciNumber
	movl	%eax, 12(%rsp)
	movl	%eax, %edi
	callq	_print_int
	addq	$24, %rsp
	retq
	.cfi_endproc
                                        ## -- End function
	.section	__DATA,__data
	.globl	_prt_1                          ## @prt_1
	.p2align	2, 0x0
_prt_1:
	.long	17                              ## 0x11

.subsections_via_symbols
