# i8kfans

Adjust the fans speed in various Dell laptops (with a nvidia graphics card) to
maintain the right temperatures. This affect both fans, the cpu and the gpu
fan. Originally i8k was created to run in a Dell Inspiron 8000 laptop, but this
Dell fan control via SMM BIOS is available in others laptops of various series
(Inspiron, XPS, Latitude, etcetera), but not all of them are supported. Mine is
an Inspiron 9400 but I tested this successfully in a XPS m1330 too.

Based on a 2006 bash script by Wheelspin, `i8kapplet`. This old script served
faithfully me for many years, but my ears couldn't stand much longer its random
and common slow downs/speed ups. Over the years, fans have become more and more
loud. This new script runs in a more smooth way, with less sudden changes.
It's cheaper than replace booth fans, don't you think?

This script needs the `i8kutils` linux package installed and the `i8k` kernel
module loaded to work.


