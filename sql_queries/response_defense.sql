select GAME.seas, GAME.wk, DEFENSE.team,
	sum(DEFENSE.sck), sum(DEFENSE.saf), sum(DEFENSE.blk), sum(DEFENSE.ints), sum(DEFENSE.frcv),
	sum(DEFENSE.tdd), sum(DEFENSE.tdret),
    if(DEFENSE.team = GAME.v, avg(GAME.ptsh), avg(GAME.ptsv)) as pts_allow
from DEFENSE
left join GAME
	on DEFENSE.gid = GAME.gid
where GAME.wk <= 17
group by GAME.seas, GAME.wk, DEFENSE.team, GAME.v, GAME.h
;