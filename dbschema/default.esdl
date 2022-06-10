module default {
  scalar type AccessMode extending enum<public, private>;

  abstract type Auditable {
    property created_at -> datetime {
      readonly := true;
      default := datetime_current();
    }
  }

  type Counter extending Auditable {
    required property name -> str;
    required property owner_id -> str;
  }
}
