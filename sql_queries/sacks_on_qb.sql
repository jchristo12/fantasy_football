select concat(GAME.seas, "&", GAME.wk, "&", SACK.qb) as pk,
	GAME.seas, GAME.wk, SACK.qb, count(SACK.pid) as tot_sack
from SACK
left join PLAY
	on SACK.pid = PLAY.pid
left join GAME
	on PLAY.gid = GAME.gid
where GAME.wk <= 17
group by GAME.seas, GAME.wk, SACK.qb
-- limit 10
;