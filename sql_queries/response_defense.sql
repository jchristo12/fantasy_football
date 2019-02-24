select concat(GAME.gid, "&", DEFENSE.team) as pk,
	GAME.gid, GAME.seas, GAME.wk, DEFENSE.team,
	sum(DEFENSE.sck) as sck, sum(DEFENSE.saf) as saf, sum(DEFENSE.blk) as blk, 
    sum(DEFENSE.ints) as ints, sum(DEFENSE.frcv) as frcv, sum(DEFENSE.tdd) as tdd,
    sum(DEFENSE.tdret) as tdret,
    if(DEFENSE.team = GAME.v, avg(GAME.ptsh), avg(GAME.ptsv)) as pts_allow
from DEFENSE
left join GAME
	on DEFENSE.gid = GAME.gid
where GAME.wk <= 16
group by GAME.gid, GAME.seas, GAME.wk, DEFENSE.team, GAME.v, GAME.h
-- limit 10
;