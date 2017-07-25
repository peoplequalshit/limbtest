c=============================================================================!
c=============================================================================!
      program secondary_spectra
      implicit none
      integer i,iap,iat
      double precision E1,E2,s,apspec

      call init

c  apspec(e0,epbar,iap,iat) returns Epbar * d[sig(E0,Epbar)]  / d[Epbar]
c  in mbarn for primary nuclei with mass number iap =1,..,60, 
c  target nuclei with mass number iat =1,4; 
c  all energies are (relativistic) energy per nucleon in GeV


      iap=1 
      iat=1
      E1=100.d0

      open(21,file='aprot.dat')
      do i=1,200,1
         E2 = 0.979**i * E1
         s = apspec(E1,E2,iap,iat)
         write(21,*) real(E2),real(s)
      end do
      close(21)

      end program secondary_spectra
