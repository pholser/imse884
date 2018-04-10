/* --------------------------------------------------------------------------
 * File: mipex1.c
 * Version 12.5
 * --------------------------------------------------------------------------
 * Licensed Materials - Property of IBM
 * 5725-A06 5725-A29 5724-Y48 5724-Y49 5724-Y54 5724-Y55 5655-Y21
 * Copyright IBM Corporation 1997, 2012. All Rights Reserved.
 *
 * US Government Users Restricted Rights - Use, duplication or
 * disclosure restricted by GSA ADP Schedule Contract with
 * IBM Corp.
 * --------------------------------------------------------------------------
 */

/* mipex1.c - Entering and optimizing a MIP problem */

/* Bring in the CPLEX function declarations and the C library
   header file stdio.h with the include of cplex.h. */
#include <ilcplex/cplex.h>

/* Bring in the declarations for the string functions */



#include <time.h>
#include <ctype.h>

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "math.h"
#include "defines.h"

#define ROWS 5
#define VARS 250


int addlecut (CPXENVptr env, CPXLPptr  lp, int *clique, double *value, double  right) ;
int solvemylp (CPXENVptr env, CPXLPptr  lp,  double *x) ;
void generatelp (CPXENVptr env, CPXLPptr lp) ;
void changetoip (CPXENVptr env, CPXLPptr lp) ;
int solvemymip (CPXENVptr env, CPXLPptr  lp,  double *x) ;

static double z;

int main(void)
{

    double   *x     = NULL, *reduce=NULL; 
    CPXENVptr     env = NULL;
    CPXLPptr      lp = NULL;
    int           status, solstat, *indices, store;
    int           i,j,numrows, curr_cols, numvar, sum;
    double      *values,  cutrhs, temp;
    int amatrix[5][250];
    int rhs[5];
    int obj[250];

    FILE *fp;
   
    numvar=VARS;
    numrows=ROWS;
    srand(17171);
   
//  Get a CPLEX license

    env = CPXopenCPLEX (&status);

   
    if ( env == NULL ) {
        char  errmsg[1024];
        fprintf (stderr, "Could not open CPLEX environment.\n");
        CPXgeterrorstring (env, status, errmsg);
        fprintf (stderr, "%s", errmsg);
        goto TERMINATE;
    }
    
   /* Turn on output to the screen */
  
   status = CPXsetintparam (env, CPX_PARAM_SCRIND, CPX_ON);
   if ( status ) {
        fprintf (stderr, "Failure to turn on screen indicator, error %d.\n", status);
        goto TERMINATE;
   }
  
    /* Create the problem, using the filename as the problem name */
  
   lp = CPXcreateprob (env, &status, "problem");
 
   if ( lp == NULL ) {
        fprintf (stderr, "Failed to create LP.\n");
        goto TERMINATE;
   }
  
//  Read in the problem from the file mk.lp  See this file for the format.
 
   for (i=0; i<numrows; i++){
       sum=0;
       for (j =0; j<numvar; j++) {
           store=rand();
           temp=(double)store/RAND_MAX;
           temp=temp*1000;
           store=(int) temp;
           if (store==0) store=1;
           amatrix[i][j]=store;
           sum+=amatrix[i][j];
           printf("%d\t", store);
       }
       rhs[i]=(int) sum/20;
   }
   for (j=0; j<numvar; j++){
       sum=0;
       for (i=0; i<numrows; i++){
           sum+=amatrix[i][j];
       }
       store=rand();
       temp=(double)store/RAND_MAX;
       temp=temp*200;
       store=(int) temp;
	   obj[j]=sum+store;
   }

   fp = fopen("mk.lp", "w");
   fprintf(fp, "Maximize\n");
   for(j=0; j<numvar; j++) {
       if (j<numvar-1){
           if (j%10==9) fprintf(fp,"\n");
           fprintf(fp,"%d x%d +", obj[j], j);
       } else {
           fprintf(fp,"%d x%d\n", obj[j], j);
       }
   }
   fprintf(fp, "Subject to\n");
   for(i=0; i<numrows; i++) {
       for(j=0; j<numvar; j++) {
           if (j%10==9) fprintf(fp,"\n");
           if (j<numvar-1){
               fprintf(fp,"%d x%d +", amatrix[i][j], j);
           } else {
               fprintf(fp,"%d x%d<=%d\n", amatrix[i][j], j, rhs[i]);
           }
       }
   }


   fprintf(fp, "Bounds\n");
   for(j=0; j<numvar; j++) {
      fprintf(fp," 0<=x%d<=1\n ", j);
   }
   fprintf(fp, "End\n");
   fclose(fp);
   
   getchar();

   status = CPXreadcopyprob (env, lp, "mk.lp" , NULL);
     if ( status ) {
        fprintf (stderr, "Failed to read and copy the problem data.\n");
        goto TERMINATE;
     } 

//  Set up the problem manually in CPLEX (this is done in columns
    
    //generatelp ( env, lp);


//  Allocate memory for the solution.  Note that the cplex command returns the number
//     of collumns.
     numvar=CPXgetnumcols(env, lp);
     x = (double *) malloc (CPXgetnumcols(env, lp)*sizeof(double));
     
     if ( x == NULL ) {
        fprintf (stderr, "No memory for solution values.\n");
        goto TERMINATE;
 
     }
//here I get the LP relaxation solution
     solvemylp (env, lp,  x);
     printf("The objective value is %f\n", z);
     for (i=0; i<CPXgetnumcols(env, lp); i++) {
         printf("x%d = %f\n",i, x[i]);
     }
     getchar();


     // This section will adds a cuts
     indices = (int *) malloc (CPXgetnumcols(env, lp)*sizeof(int));
     values = (double *) malloc (CPXgetnumcols(env, lp)*sizeof(double));
//I will add the constraint sum of 2x0+...+2x50<=2

     for (i=0; i<51; i++) {
         indices[i]=i;
         values[i]=2;
     }
     cutrhs=2;
     indices[i]=-1;
     values[i]=-1;

     addlecut(env, lp,indices, values, cutrhs); // adds the cut;


// I will add the constraint 2x0+x3<=2;
/*
     indices[0]=0;
     indices[1]=3;
     indices[2]=-1;

     values[0]=2;
     values[1]=1;
     values[2]=-1;

     rhs=2;
     addlecut(env, lp,indices, values, rhs); // adds the cut;
*/

     getchar();//this waits for the user to add hit an enter.

     


// I will add the constraint sum of all xi <=3;
/*     for (i=0; i<CPXgetnumcols(env, lp); i++) {
         indices[i]=i;
         values[i]=1.0;
     }
     indices[i]=-1;
     values[i]=-1;
     rhs=2.0;    
     addlecut(env, lp,indices, values, rhs); 
*/     
    changetoip (env,lp);


// This solves an IP and returns the z and the x's (both doubles).

    
     solvemymip (env, lp,  x);

     for (i=0; i<CPXgetnumcols(env, lp); i++) {
         printf("x%d = %f\n",i, x[i]);
     }
    

TERMINATE:
  
        
     /* Free up the problem as allocated by CPXcreateprob, if necessary */
    
     printf("The total time is %d seconds\n", (int) (clock()/ CLOCKS_PER_SEC));
    
     if ( lp != NULL ) {
        status = CPXfreeprob (env, &lp);
        if ( status ) {
           fprintf (stderr, "CPXfreeprob failed, error code %d.\n", status);
        }
     }
  

     /* Free up the CPLEX environment, if necessary */
  
     if ( env != NULL ) {
        status = CPXcloseCPLEX (&env);
  
        /* Note that CPXcloseCPLEX produces no output,
           so the only way to see the cause of the error is to use
           CPXgeterrorstring.  For other CPLEX routines, the errors will
           be seen if the CPX_PARAM_SCRIND indicator is set to CPX_ON. */
  
        if ( status ) {
        char  errmsg[1024];
           fprintf (stderr, "Could not close CPLEX environment.\n");
           CPXgeterrorstring (env, status, errmsg);
           fprintf (stderr, "%s", errmsg);
        }
     }

	
	return 0;
}






void generatelp (CPXENVptr env, CPXLPptr lp) {

    
    int i, rows, cols, cnt, j, *index, status;
    double *obj, *rhs, *lb, *ub, store;
    char *sense;
    int *matcnt, *matbeg;
    int *matind;
    double *matval, *matrng;



    rows= 3;
    cols= 4;

/*  This routine writes either an IP or an LP of the form

    Minimize 3w+4x+8y+9z
    s.t.     w+x-5z <=0
             w+x +2z =3
             w+x+y+z >=1

*/
//    printf("rows =%d, cols=%d", rows, cols);
    MYCALLOC(matind,int,2*rows*cols+1+2);
    MYCALLOC(matbeg,int,2*cols+2);
    MYCALLOC(matcnt,int,2*cols+2);
    MYCALLOC(obj, double,cols+2);
    MYCALLOC(rhs, double,2*rows+1);
    MYCALLOC(matrng, double,rows+1);
    MYCALLOC(lb, double,cols+1);
    MYCALLOC(ub, double,cols+1);
    MYCALLOC(matval, double,2*rows*cols+1+5);
    MYCALLOC(sense, char,rows+1);
  
    //set up the lower bounds, upper bounds, objective coef, righthand side, and the sign of the 
    // constraint, which is given by the first Capital letter.

    for (i=0; i<cols; i++) {
        lb[i]=0;
        ub[i]=1;
    }
    obj[0]=3;
    obj[1]=4;
    obj[2]=8;
    obj[3]=9;

    rhs[0]=0;
    rhs[1]=3;
    rhs[2]=1;
    sense[0]='L';
    sense[1]='E';
    sense[2]='G';

    //put in the w and x columns
    
    cnt=0;
    for (j=0; j<2; j++) {
        matbeg[j] = cnt;
        matcnt[j]=3;
        for (i=0; i<rows; i++){
            matval[cnt]=1.0;
            matind[cnt]=i;
            cnt++;
        }
    }  
    
    //put in the y column
    
    matbeg[j]=cnt;
    matcnt[j]=1;
    matval[cnt]=1.0;
    matind[cnt]=1;
    cnt++;
    j++;
    
    //put in the z column

    matbeg[j]=cnt;
    matcnt[j]=3;
    matval[cnt]=-5.0;
    matind[cnt]=0;
    cnt++;
    matval[cnt]=2.0;
    matind[cnt]=1;
    cnt++;
    matval[cnt]=1.0;
    matind[cnt]=2;
    cnt++;
    j++;
    //Let CPLEX know the ending location.
    matbeg[j]=cnt;

    // 1 is for min

    status = CPXcopylp (env, lp, cols, rows, 1 , obj,rhs,
                        sense,matbeg, matcnt, matind, matval,lb, ub,matrng);
   
    
    if (status) {
        printf("Did not add the LP");
        getchar();
    }   
    
    free(matind);
    free(matbeg);
    free(obj);
    free(rhs);
    free(matrng);
    free(lb);
    free(ub);
    free(matval);
    free(sense);

}

void changetoip (CPXENVptr env, CPXLPptr lp) {

//  This changes the problem from an LP to an IP.

    int *indices, status,i;
    char *ctype;

    indices = (int *) malloc (CPXgetnumcols(env, lp)*sizeof(int));
    ctype  = (char *) malloc (CPXgetnumcols(env, lp)*sizeof(double));

    for (i=0; i<CPXgetnumcols(env, lp); i++) {
        indices[i]=i;
        ctype[i]='B';
    }

  //  status = CPXchgprobtype (env,lp,CPXPROB_MIP);

    if (status) {
        printf("Did not add change the problem");
        getchar();
    }   

    status = CPXchgctype (env, lp, CPXgetnumcols(env, lp),indices, ctype);

    if (status) {
        printf("Did not add change the variables");
        getchar();
    }   

}


int solvemymip (CPXENVptr env, CPXLPptr  lp,  double *x) {
    
   int worked=TRUE, cur_numcols, status, solstat;

   /* set parameters before solving.  In order they are the
   relative gap, absolute gap, do not use a heuristic to look
   for integer solutions pg 163 manual, lower and upper cut offs
   how frequent to print out the node solutions*/

    CPXsetintparam(env,   CPX_PARAM_COVERS  , 2); /*interval of the node files to print out*/ 
    CPXsetintparam(env,CPX_PARAM_CLIQUES , 2); /*interval of the node files to print out*/ 
    CPXsetintparam(env,CPX_PARAM_GUBCOVERS  , 2); /*interval of the node files to print out*/ 
   CPXsetdblparam(env,CPX_PARAM_EPGAP, 0.0000001);
//   CPXsetdblparam(env,CPX_PARAM_EPAGAP,1.0);
   CPXsetintparam(env,CPX_PARAM_HEURFREQ,-1);
   CPXsetdblparam(env,CPX_PARAM_CUTUP,1e+75);
   CPXsetdblparam(env,CPX_PARAM_CUTLO,1e-75); /*best feasible solution value for max*/ 
   CPXsetintparam(env,CPX_PARAM_MIPINTERVAL, 10000); /*interval of the node files to print out*/ 

   
   status = CPXmipopt (env, lp);

   if ( status ) {
      fprintf (stderr, "Failed to optimize MIP.\n");
      worked=FALSE;
   }
   if (worked==TRUE){
       solstat = CPXgetstat (env, lp);
       printf ("Solution status %d.\n", solstat);
       status = CPXgetmipobjval (env, lp, &z);
       if ( status ) {
          fprintf (stderr,"Failed to obtain objective value.\n");
          worked=FALSE;
       }
       if (worked==TRUE){
          printf ("Objective value %.10g\n", z);
  
     /* The size of the problem should be obtained by asking CPLEX what
        the actual size is. cur_numcols stores the current number 
        of columns. */
  
          cur_numcols = CPXgetnumcols (env, lp);
          status = CPXgetmipx (env, lp, x, 0, CPXgetnumcols(env, lp)-1);
          if ( status ) {
              fprintf (stderr, "Failed to obtain solution.\n");
              worked=FALSE;
          }
      }
   }
   return (worked);
}  


//This will solve an lp and put the solution in z or x
//*******************************************************************************
//   Solves LP with Cplex

int solvemylp (CPXENVptr env, CPXLPptr  lp,  double *x) {
    
   int worked=TRUE, cur_numcols, status, solstat;

   /* Optimize the problem and obtain solution. */
   status = CPXlpopt (env, lp);
   if ( status ) {
      fprintf (stderr, "Failed to optimize MIP.\n");
      worked=FALSE;
   }
   if (worked==TRUE){
       solstat = CPXgetstat (env, lp);
       printf ("Solution status %d.\n", solstat);
       status = CPXgetobjval (env, lp, &z);
       if ( status ) {
          fprintf (stderr,"Failed to obtain objective value.\n");
          worked=FALSE;
       }
       if (worked==TRUE){
          printf ("Objective value %.10g\n", z);
  
     /* The size of the problem should be obtained by asking CPLEX what
        the actual size is. cur_numcols stores the current number 
        of columns. */
  
         cur_numcols = CPXgetnumcols (env, lp);
         status = CPXgetx (env, lp, x, 0, CPXgetnumcols(env, lp)-1);
         if ( status ) {
             fprintf (stderr, "Failed to obtain solution.\n");
             worked=FALSE;
         }
      }
   }
    return(worked);
}  


// This will add a cut of the form sum i = 1 to end of array (denoted by -1) value[i]*x[clique[i] <=right);

int addlecut (CPXENVptr env, CPXLPptr  lp, int *clique, double *value, double  right) {
    int i,status;
    int ccnt=0,rcnt,nzcnt;
    double rhs[2];
    char sense[2];
    int *rmatbeg;
    int *rmatind;
    double *rmatval;


    rmatbeg = (int *) malloc ((1+CPXgetnumcols(env, lp))*sizeof(int));
    rmatind = (int *) malloc ((1+CPXgetnumcols(env, lp))*sizeof(int));
    rmatval = (double *) malloc ((1+CPXgetnumcols(env, lp))*sizeof(double));


    rcnt=1;
    nzcnt=0;
    rhs[0]=(double) right;

    sense[0]='L';
    i=0;
    while (clique[i]!=-1){
        rmatind[nzcnt]=clique[i];
        rmatval[nzcnt]=value[i];
        nzcnt++;
        i++;
    }
    rmatbeg[0]=0;
    rmatbeg[1]=nzcnt;
//    printf("the num of rows %d", CPXgetnumrows(env,lp));
    status = CPXaddrows (env, lp, ccnt, rcnt, nzcnt, rhs,
                       sense, rmatbeg, rmatind, rmatval,
                       NULL, NULL);

    if (status) {
        printf("failed to add the row\n");
        status=FALSE;
    } else status=TRUE;
  /*  free(rmatbeg);
    free (rmatind);
    free(rmatval);
    free(sense);
    free(rhs);
    printf("hi");*/

    return (status);
}

