select concat(GAME.gid, "&", SACK.qb) as pk,
	GAME.gid, GAME.seas, GAME.wk, SACK.qb, count(SACK.pid) as tot_sack
from SACK
left join PLAY
	on SACK.pid = PLAY.pid
left join GAME
	on PLAY.gid = GAME.gid
where GAME.wk <= 16
group by GAME.gid, GAME.seas, GAME.wk, SACK.qb
-- limit 10
;