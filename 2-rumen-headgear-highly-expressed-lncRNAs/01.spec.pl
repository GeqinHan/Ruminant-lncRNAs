#!/usr/bin/perl
use strict;
use Data::Dumper;
use List::Util qw(max);
die "Usage: perl $0 <tissueType> <exprTable> <output_Expr.tau>\n" unless @ARGV == 3;
open (IN0, "$ARGV[0]") or die "TissueType required!\n";
open (IN1, "$ARGV[1]") or die "ExprTable required!\n";
open (OUT, ">$ARGV[2]") or die "permission denied!\n";


=pod
---> TissueType File, Tab or space split
Diges~salivary_gland_adult~SRR1638782   salivary_gland
Diges~salivary_gland_adult~SRR8703157   salivary_gland
Diges~esophagus_adult~SRR8703175        esophagus
Diges~rumen_0day~SRR2777522     rumen
Diges~rumen_7days~SRR2777525    rumen
Diges~rumen_21days~SRR2777529   rumen

---> ExprTable File, Tab split
chr     start   end     gene    Diges~salivary_gland_adult~SRR1638782   Diges~salivary_gland_adult~SRR8703157   Diges~esophagus_adult~SRR8703175        Diges~gall_bladder_adult~SRR1639233 Diges~gall_bladder_adult~SRR8703177      Diges~liver_adult~SRR3168798    Diges~liver_adult~SRR3168796    Diges~liver_adult~SRR3168793
1       207958  209108  LOC112447009    0.00    0.00    0.00    0.00    0.00    0.03    0.03    0.17
7       42117978        42118946        OR2T2   0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00
7       42235853        42236806        LOC788323       0.00    0.00    0.00    0.00    0.00    0.00    0.00    0.00
=cut

my %type;
while(<IN0>){
	chomp; 
	my @A=split/\s+/; 
	$type{$A[0]}=$A[1];
}

my %group;
my $h=<IN1>; 
chomp($h); 
my @B=split/\t/, $h; 
for(my $i=4; $i<@B; $i++){
	push @{$group{$type{$B[$i]}}}, $i;
}

#print Dumper(%group),"\n";
print OUT "tau","\t",$h,"\n";

while(<IN1>){
	chomp;
	my @C=split/\t/; 
	my $FPKM_Ecount=0;
	my @line;
	for(my $j=4; $j<@C; $j++){
		if($C[$j] < 1){
			$C[$j] = 1;
		}
		$C[$j] = log($C[$j])/log(2);
		if($C[$j] >0){
			$FPKM_Ecount ++;
		}
	} 
	
	foreach my $grp_tmp(keys %group){
		#print $grp_tmp,"~", join("\t",@{$group{$grp_tmp}}),"\n";
		my $tisMax = max (@C[@{$group{$grp_tmp}}]);
		push @line, $tisMax;
	}
	if($FPKM_Ecount > 0){
		my $lineMax = max @line;
		my $sum = 0;
		for(my $k=0; $k<@line; $k++){
			my $k_i = $line[$k]/$lineMax;
			$sum += (1 - $k_i);
		}
		my $tau = $sum/(@line - 1);			
		$tau = sprintf("%.5f", $tau);
		print OUT $tau,"\t",$_,"\n";
	}else{
		print OUT "NA","\t",$_,"\n";
	}												                	           }
close IN0;
close IN1;
close OUT;
