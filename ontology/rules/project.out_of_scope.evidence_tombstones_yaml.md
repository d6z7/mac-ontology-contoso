# project.out_of_scope.evidence_tombstones_yaml

Why evidence/tombstones.yaml is out of scope. The file moved out of governance/ in the v3 migration
(MIGRATION_NEEDS #20: outside the v3 layout); its 38 entries name 0.3.x/0.4.0 object ids and their
successors. Converting them into rule `retires` entries needs a choice of the rule that carries each one,
which the migration did not make.

## Cites

- `project`
