select concat(OFFENSE.gid, "&", OFFENSE.player) as pk,
	-- identifying features
    OFFENSE.gid, GAME.seas, GAME.wk, OFFENSE.player, OFFENSE.team, PLAYER.pos1,
    -- passing stats
    OFFENSE.pa, OFFENSE.pc, OFFENSE.py, OFFENSE.ints, OFFENSE.tdp,
    -- rushing stats
    OFFENSE.ra, OFFENSE.sra, OFFENSE.ry, OFFENSE.tdr, OFFENSE.fuml,
    -- receiving stats
    OFFENSE.trg, OFFENSE.rec, OFFENSE.recy, OFFENSE.tdrec,
    -- other stats
    OFFENSE.seas, PLAYER.height, PLAYER.weight, PLAYER.dob, PLAYER.dv,
    -- rookie combine stats
    PLAYER.forty, PLAYER.bench, PLAYER.vertical, PLAYER.broad, PLAYER.shuttle, PLAYER.cone,
		PLAYER.arm, PLAYER.hand
from OFFENSE
left join GAME
	on OFFENSE.gid = GAME.gid
left join PLAYER
	on OFFENSE.player = PLAYER.player
where GAME.wk <= 16
-- limit 10
;