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
  <path d="M28.427,20.917l-0.51,0.51l2.214,2.213H23.36V8.36H31V7.64h-7.64V1c0-0.199-0.161-0.36-0.36-0.36H11	c-0.199,0-0.36,0.161-0.36,0.36v30c0,0.199,0.161,0.36,0.36,0.36h12c0.199,0,0.36-0.161,0.36-0.36v-6.64h6.771l-2.214,2.213	l0.51,0.51L31.509,24L28.427,20.917z M22.64,30.64H11.36V1.36h11.28v6.28H17v0.72h5.64v15.28H17v0.721h5.64V30.64z M1,23.64h7.616	v0.721H1V23.64z M1.869,7.64h6.747v0.72H1.869l2.214,2.214l-0.509,0.509L0.491,8l3.083-3.083l0.509,0.509L1.869,7.64z"></path>
</svg>