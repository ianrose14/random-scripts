#!/usr/bin/perl
#
$filename=@ARGV[0];
(($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size,$atime,$mtime,$ctime,$blksize,$blocks) = lstat($filename));
printf("atime is %d\n",$atime);
printf("mtime is %d\n",$mtime);
printf("ctime is %d\n",$ctime);
printf("Name is %s\n",$filename);
