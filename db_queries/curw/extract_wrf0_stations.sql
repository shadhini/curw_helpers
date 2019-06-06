select `id`, `latitude`, `longitude` from `station` where name like 'wrf$_%' ESCAPE '$' and name not like 'wrf$_v3%' ESCAPE '$';
