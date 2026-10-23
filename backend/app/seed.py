"""Creates a sample record in every table and verifies foreign-key relationships.

Run from the backend/ folder:  python -m app.seed
"""
from sqlalchemy import inspect, select

from app.database import SessionLocal, engine
from app.models import (
    AuditLog, Environment, EvaluationStat, Flag, FlagVersion,
    TargetingRule, User, UserGroup, UserGroupMembership,
)

EXPECTED_TABLES = {
    "users", "environments", "flags", "flag_versions", "user_groups",
    "user_group_memberships", "targeting_rules", "audit_log", "evaluation_stats",
}


def verify_tables() -> None:
    existing = set(inspect(engine).get_table_names())
    missing = EXPECTED_TABLES - existing
    if missing:
        raise SystemExit(f"Missing tables: {sorted(missing)}. Run: alembic upgrade head")
    print(f"[OK] All {len(EXPECTED_TABLES)} required tables exist.")


def seed() -> None:
    from datetime import date

    with SessionLocal() as db:
        if db.scalar(select(User).where(User.email == "admin@example.com")):
            print("[SKIP] Sample data already exists.")
            return

        user = User(name="Admin User", email="admin@example.com",
                    password_hash="placeholder-hash-replaced-in-milestone-2", role="admin")
        env = Environment(name="development", description="Development environment")
        group = UserGroup(name="beta_users", description="Beta testers")
        db.add_all([user, env, group])
        db.flush()

        flag = Flag(environment_id=env.id, key="new_checkout", type="boolean",
                    default_value=False, enabled=True,
                    description="New checkout flow", owner_team="payments", created_by=user.id)
        db.add_all([UserGroupMembership(user_id=user.id, group_id=group.id), flag])
        db.flush()

        db.add_all([
            FlagVersion(flag_id=flag.id, version_number=1,
                        configuration={"enabled": True, "default_value": False}, created_by=user.id),
            TargetingRule(flag_id=flag.id, rule_type="group", operator="in",
                          attribute="group", value=["beta_users"], result=True, priority=1),
            AuditLog(user_id=user.id, flag_id=flag.id, action="flag.create",
                     before_value=None, after_value={"key": "new_checkout", "enabled": True}),
            EvaluationStat(flag_id=flag.id, environment_id=env.id,
                           date=date.today(), hour=10, evaluation_count=1),
        ])
        db.commit()

        # Verify foreign-key relationships through the ORM
        db.refresh(flag)
        assert flag.environment.name == "development"
        assert flag.creator.email == "admin@example.com"
        assert len(flag.versions) == 1 and len(flag.targeting_rules) == 1
        assert len(flag.audit_logs) == 1 and len(flag.evaluation_stats) == 1
        assert user.group_memberships[0].group.name == "beta_users"
        print("[OK] Sample records inserted and foreign-key relationships verified.")


if __name__ == "__main__":
    verify_tables()
    seed()
