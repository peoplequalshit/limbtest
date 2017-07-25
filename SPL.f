! systematic condition
      implicit double precision (a-h,o-z)
      integer reac
      double precision Eg,lEg,dLEg,Ep,lEp,dlEp,y,dummy,norm,gamma,gamma1
      double precision gamma2,Ebreak,mp,powerlaw,powerlaw1,powerlaw2
      double precision normAll
      double precision par(5)
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
      norm=par(1)
      gamma1=par(2)
      gamma2=par(3)
      Ebreak=par(4)
      normAll=par(5)
! my condition
      mp=0.938
      Nbinsg=50
      lEming=1
      lEmaxg=3
      Nbinsp=50
      lEminp=1
      lEmaxp=6
      gamma=gamma1            !suppose SPL
! test multiple file
      gamma=gamma1
      write(fn,fmt='(i0,a)') k, '.dat'
      open(2,file=fn,form='formatted')
! start mycode
      print *,'gamma=',gamma
      dlEg=log(10.0)*(1.0/Nbinsg)
      dlEp=log(10.0)*(1.0/Nbinsp)
      do i=lEming,(Nbinsg*(lEmaxg-lEming))+1
       Eg=10.0**(lEming+((i-1.0)/Nbinsg))
       y=0
       do j=lEminp,(Nbinsp*(lEmaxp-lEminp))+1
        Ep=(10.0)**(lEminp+((j-1.0)/Nbinsp))
        if (Ep>Eg) then
         fff=spec_int(Ep,Eg,id,reac)
         powerlaw1=norm*(Ep*(Ep+(2.0*mp)))**(-0.5*gamma1)
         powerlaw2=(Ep+mp)/sqrt(Ep*(Ep+(2.0*mp)))
         powerlaw=powerlaw2*powerlaw1
         sum=(Ep/Eg)*powerlaw*fff*dlEp
         y=y+sum
        endif
       enddo
       write(2,*) Eg,y*normAll ! 
      enddo
      close(2)
      end
