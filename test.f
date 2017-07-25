! systematic condition
      implicit double precision (a-h,o-z)
      integer reac
      character(len=70) fn
      character(len=20) :: arg
      call spec_init
      reac=0
      ep=1.d2                   !100 GeV incident proton                     
      id=0                      !photon spectrum                             

      do i=1,100
       x=i/100.d0-.005d0
       es=x*ep
       fff=spec_int(ep,es,id,reac)
       print *,x,fff
      enddo
      end
