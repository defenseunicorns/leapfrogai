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
  <path d="M31,31.36H1v-0.72h1.64V18h0.72v12.64h9.28V23c0-0.199,0.161-0.36,0.36-0.36h6	c0.199,0,0.36,0.161,0.36,0.36v7.64h9.279V18h0.721v12.64H31V31.36z M13.36,30.64h5.28v-7.28h-5.28	C13.36,23.36,13.36,30.64,13.36,30.64z M26.36,21h-0.72v-3h0.721L26.36,21L26.36,21z M22.36,21h-0.72v-3h0.721L22.36,21L22.36,21z M10.36,21H9.64v-3h0.72C10.36,18,10.36,21,10.36,21z M6.36,21H5.64v-3h0.72C6.36,18,6.36,21,6.36,21z M31,15.36H1	c-0.112,0-0.217-0.052-0.286-0.141c-0.068-0.089-0.091-0.204-0.062-0.312l2.412-9C3.106,5.75,3.249,5.64,3.412,5.64H5.64V1h0.72	v4.64h22.228c0.163,0,0.306,0.109,0.348,0.267l2.412,9c0.029,0.108,0.006,0.224-0.062,0.312C31.218,15.308,31.112,15.36,31,15.36z M1.469,14.64h29.062l-2.22-8.28H3.688L1.469,14.64z"></path>
</svg>