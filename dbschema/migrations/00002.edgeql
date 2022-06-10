CREATE MIGRATION m1wrxjwzxjp4qdci33343g667qun43tfef7ryeobx65vig2lmgf6oa
    ONTO m1pvaaovzugta4kmuo2erusoangqxcyjwboxfr3swlxq6pcq3fafgq
{
  ALTER TYPE default::Counter {
      DROP PROPERTY access_mode;
  };
};
