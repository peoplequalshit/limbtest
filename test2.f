! systematic condition
      implicit double precision (a-h,o-z)
      integer reac
      double precision Eg,lEg,dLEg,Ep,lEp,dlEp,y,dummy,norm,gamma1,gamma2,Ebreak
      double precision par(4)
      character(len=70) fn
      character(len=20) :: arg

      call spec_ini                !initialization

      reac=0                       !pp collision, combined Kamae+QGSJET
      id=0                         !photon spectrum

      do i=1,iargc()
       call getarg(i,arg)
       read(arg,*) par(i)
      enddo
      print *,par(1)

      end
