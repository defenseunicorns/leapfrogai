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
  <path d="M30,30.36h-7v-0.72h6.64V14h0.721v16	C30.36,30.199,30.199,30.36,30,30.36z M18,30.36H2c-0.199,0-0.36-0.161-0.36-0.36v-7h0.72v6.64H18V30.36z M11,23.36	c-0.062,0-0.124-0.017-0.179-0.048C10.709,23.248,10.64,23.129,10.64,23V9c0-0.129,0.069-0.248,0.181-0.312	c0.111-0.065,0.249-0.064,0.36,0.001l12,7c0.11,0.064,0.179,0.183,0.179,0.311s-0.068,0.247-0.179,0.311l-12,7	C11.125,23.344,11.062,23.36,11,23.36z M11.36,9.627v12.746L22.285,16L11.36,9.627z M2.36,18H1.64V2c0-0.199,0.161-0.36,0.36-0.36h7	v0.72H2.36V18z M30.36,9h-0.72V2.36H14V1.64h16c0.199,0,0.36,0.161,0.36,0.36V9z"></path>
</svg>