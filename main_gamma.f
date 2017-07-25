! example main
      implicit double precision (a-h,o-z)
      integer reac

      call spec_ini                !initialization
      
      reac=0                       !pp collision, combined Kamae+QGSJET
      ep=1.d2                      !100 GeV incident proton
      id=0                         !photon spectrum
      open(2,file='p+p-gamma0.dat')
       do i=1,100
        x=i/100.d0-.005d0
        es=x*ep
        fff=spec_int(ep,es,id,reac)
        write(2,*)x,fff
       enddo
      close (2)

      reac=1                       !pp collision, only QGSJET
      ep=1.d2                      !100 GeV incident proton
      id=0                         !photon spectrum
      open(2,file='p+p-gamma1.dat')
       do i=1,100
        x=i/100.d0-.005d0
        es=x*ep
        fff=spec_int(ep,es,id,reac)
        write(2,*)x,fff
       enddo
      close (2)
      
      reac=3                       !He-p collision, only QGSJET
      ep=1.d2                      !400 GeV incident helium (100 GeV/nucleon)
      id=0                         !photon spectrum
      open(2,file='He+p-gamma.dat')
       do i=1,100
        x=i/100.d0-.005d0
        es=x*ep
        fff=spec_int(ep,es,id,reac)
        write(2,*)x,fff
       enddo
      close (2)
      
      end   

