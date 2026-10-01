# Read workspace context without treating first use as an error

Read only the known files in the user-selected workspace. Missing is normal;
unreadable is a retrieval limitation, not proof that no context exists. Reuse
current conversation and accessible memory before asking for company details.
Do not search other folders or replace an existing brief with an empty template.

When Node and a shell are available, substitute the chosen workspace below and
run this read-only command. It returns a separate status for each expected file.
Otherwise use the client's existence/read tools with the same distinctions.

```sh
node --input-type=module - '/absolute/path/to/chosen-workspace' <<'JS'
import { readFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
const workspace = resolve(process.argv[2] || process.cwd());
const paths = ['brief.md', 'cmo/brief.md', 'cmo/plan.md', 'cmo/activity.md'];
const files = await Promise.all(paths.map(async path => {
  try {
    const content = await readFile(join(workspace, '.coco', path), 'utf8');
    return { path: `.coco/${path}`, status: 'present', content };
  } catch (error) {
    return {
      path: `.coco/${path}`,
      status: error.code === 'ENOENT' ? 'missing' : 'unreadable',
      ...(error.code === 'ENOENT' ? {} : { error: error.code || 'READ_FAILED' }),
    };
  }
}));
console.log(JSON.stringify({ workspace, files }));
JS
```

Before writing, compare the current company's identity/domain with the saved
briefs. For work on a different customer in the same workspace, keep that
customer's shared brief, specialist brief, plan, activity and deliverables under
`.coco/clients/<company-key>/` (with the specialist files under `cmo/`). Reuse
that location on resumption. Read before updating, preserve existing content and
user edits, and append dated activity rather than replacing its history. Never
replace the workspace owner's briefs with a customer's notes or a blank template.
An unreadable existing file must not be treated as a safe new-file destination.

Keep the shared `brief.md` short: company, goal/definition, active role and its brief
path, user mandate, deliverable links, last result and next action. Under `cmo/`,
use `brief.md` for facts and constraints, `plan.md` for current work, `activity.md`
for dated evidence and decisions, and `deliverables/` for outputs. Save after meaningful
work, preserving previous results and user edits; verify writes before claiming success.
Record sources/dates and distinguish facts from assumptions. Do not store credentials
or unnecessary personal information. Preserve `.coco/.gitignore` rules covering
`brief.md`, `cmo/` and `clients/`; never commit customer records. If persistence
fails, provide a carry-forward summary without claiming it was saved.
