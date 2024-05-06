<script>
  /**
   * Specify the pictogram title.
   * @type {string}
   */
  export let title = undefined;

  $: labelled =  $$props["aria-label"] || $$props["aria-labelledby"] || $$props["title"];
  $: attributes = {
    "aria-hidden": labelled ? undefined : true,
    role: labelled ? "img" : undefined,
    focusable: Number($$props["tabindex"]) === 0  ? true : undefined,
  };
</script>

<svg
  preserveAspectRatio="xMidYMid meet"
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 32 32"
  width="64"
  height="64"
  fill="currentColor"
  {title}
  {...attributes}
  {...$$restProps}>
  <path d="M20.36 9c0-.199-.161-.36-.36-.36h-7.64V7h-.72v1.64H1C.801 8.64.64 8.801.64 9v22c0 .199.161.36.36.36h19c.199 0 .36-.161.36-.36v-7.64H22v-.72h-1.64V9zM19.64 30.64H1.36V9.36h18.28C19.64 9.36 19.64 30.64 19.64 30.64zM12.36 1.36H14V.64h-2c-.199 0-.36.161-.36.36v2h.72C12.36 3 12.36 1.36 12.36 1.36zM16.647.64H20.177V1.3599999999999999H16.647zM22.823.64H26.352V1.3599999999999999H22.823zM31 .64h-2v.72h1.64V3h.721V1C31.36.801 31.199.64 31 .64zM30.64 13.588H31.361V17.823H30.64zM30.64 6.176H31.361V10.411000000000001H30.64zM30.64 22.64H29v.721h2c.199 0 .36-.161.36-.36v-2h-.72C30.64 21.001 30.64 22.64 30.64 22.64zM24.101 22.64H26.901V23.361H24.101z"></path>
</svg>