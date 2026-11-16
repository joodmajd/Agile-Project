export default [
  { ignores: ['node_modules/**'] },
  { files: ['**/*.js'], languageOptions: { ecmaVersion: 2024, sourceType: 'module', globals: { process:'readonly', console:'readonly', localStorage:'readonly', document:'readonly', window:'readonly', crypto:'readonly', confirm:'readonly', FormData:'readonly', Date:'readonly', Math:'readonly', URL:'readonly', structuredClone:'readonly' } }, rules: { 'no-unused-vars':'error', 'no-undef':'error', 'eqeqeq':['error','always'], 'semi':['error','always'] } }
];
