select concat(GAME.seas, "&", GAME.wk, "&", FGXP.fkicker) as pk,
	GAME.seas, GAME.wk, FGXP.fkicker, FGXP.good,
	if(FGXP.dist < 20 and FGXP.fgxp = "FG", 1, 0) as "0-19",
    if(FGXP.dist < 30 and FGXP.dist >= 20 and FGXP.fgxp = "FG", 1, 0) as "20-29",
    if(FGXP.dist < 40 and FGXP.dist >= 30 and FGXP.fgxp = "FG", 1, 0) as "30-39",
    if(FGXP.dist < 50 and FGXP.dist >= 40 and FGXP.fgxp = "FG", 1, 0) as "40-49",
    if(FGXP.dist >= 50 and FGXP.fgxp = "FG", 1, 0) as "50+",
    if(FGXP.fgxp = "XP", 1, 0) as "XP"
from FGXP
left join PLAY
	on FGXP.pid = PLAY.pid
left join GAME
	on PLAY.gid = GAME.gid
where GAME.wk <= 17
-- limit 10
;