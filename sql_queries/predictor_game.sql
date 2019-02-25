select GAME.gid, GAME.v, GAME.h,
    -- game attributes
    GAME.day, GAME.cond, GAME.stad, GAME.temp, GAME.wdir, GAME.surf, GAME.humd,
    -- betting details
    GAME.ou, GAME.sprv, GAME.ptsv, GAME.ptsh
from GAME
-- left join TEAM
	-- on GAME.gid = TEAM.gid
-- limit 10
;