#!/bin/sh
/tmp/confoto.txt; :>/tmp/sinfoto.txt; mysql -u root -p -N -B -e "use itaca; select DNI_NORM, gacadcod, nombre, apellido1, apellido2, NIA from alumnos where borrado=''" |while read d a; do if [ ! -r /var/lib/datastore/matricula/$d.jpg ] ; then OUT_FILE="/tmp/sinfoto.txt"; else OUT_FILE="/tmp/confoto.txt"; fi; echo "$d $a" >> "$OUT_FILE" ; done

