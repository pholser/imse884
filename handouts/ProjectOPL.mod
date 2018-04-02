/*********************************************
 * OPL 12.5 Model
 * Author: teaston
 * Creation Date: Apr 17, 2014 at 4:01:10 PM
 *********************************************/

int n=30;

range indices =1..n;
range rows =1..1;
range cuts = 1..3;


int A [rows,  indices] = [[382,101,596,899,885,958,14,407,863,139,245,45,32,164,220,17,285,343,554,357,372,356,910,466,426,304,976,807,991,256]];
int b[rows]= [6557];

int cover[cuts, indices]=...;
int coverrhs [cuts]=...;


/*
int A [rows, indices] = [[382,101,596,899,885,958,14,407,863,139,245,45,32,164,220,17,285,343,554,357,372,356,910,466,426,304,976,807,991,256],
[952,53,705,817,973,466,300,750,351,776,74,198,64,358,487,511,373,986,41,231,5,926,100,257,776,680,809,724,85,132]];
int+ b[rows]= [6557,6980];
*/
float objective[indices] = [789,111,369,1997,669,678,1497,756,82,1040,1632,1630,799,1346,1930,1345,1066,586,1223,984,1889,1996,67,1110,1907,1665,1155,1751,1691,915];




dvar int x[indices] in 0..1;



maximize sum(i in indices) objective[i]*x[i];

subject to {
   
   forall (j in rows) sum (i in indices) A[j,i]*x[i] <=b[j];
   forall (i in indices) x[i] <=1;
   
//This is memory allocation for the cut.

   forall (i in cuts) sum (j in indices) cover[i][j]*x[i] <=coverrhs[i];

};





main{

   //Loads this model into the project.     
   var prj=thisOplModel
   var mod=prj.modelDefinition
   
   //Loads in a data file.  Observe that the data file only has the information for the cuts
   
   var dat=prj.dataElements
   var cover=dat.cover
   var coverrhs=dat.coverrhs

  
  
   for (var i=1; i<=3; ++i){
      //clears the old model adds in the new data regenerates and solves.
      cplex.clearModel()
      prj=new IloOplModel(mod,cplex)
      prj.addDataSource(dat)
      prj.generate()
      cplex.solve()
      var cnt=0;
      var zero=0;
      writeln("solution =", cplex.getObjValue())
      for (var j in prj.indices){  
         writeln(" x ", j , " = ", prj.x[j]);
         //this generates the cut to eliminate the best solution.
         if (prj.x[j]>=.99) {
            cover[i][j]=1;
            cnt=cnt+1;
         } else {
//            cover[i][j]=-1;
            zero=zero+1;
         }
         
      }
      coverrhs[i]=cnt-1
      writeln ("rhs ", coverrhs[i], " 1s ",cnt," zero ", zero  );   
   }
   0;
}
 