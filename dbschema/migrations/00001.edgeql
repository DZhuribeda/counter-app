CREATE MIGRATION m1pvaaovzugta4kmuo2erusoangqxcyjwboxfr3swlxq6pcq3fafgq
    ONTO initial
{
  CREATE ABSTRACT TYPE default::Auditable {
      CREATE PROPERTY created_at -> std::datetime {
          SET default := (std::datetime_current());
          SET readonly := true;
      };
  };
  CREATE SCALAR TYPE default::AccessMode EXTENDING enum<public, private>;
  CREATE TYPE default::Counter EXTENDING default::Auditable {
      CREATE REQUIRED PROPERTY access_mode -> default::AccessMode;
      CREATE REQUIRED PROPERTY name -> std::str;
      CREATE REQUIRED PROPERTY owner_id -> std::str;
  };
};
