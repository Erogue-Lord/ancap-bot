CREATE TABLE "users" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"balance"	REAL NOT NULL DEFAULT 0.00,
	PRIMARY KEY("user_id")
)