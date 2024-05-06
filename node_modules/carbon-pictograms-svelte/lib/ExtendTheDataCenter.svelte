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
  <path d="M31.255,0.746	C31.188,0.678,31.096,0.64,31,0.64L1.046,0.643c-0.085-0.009-0.174,0.01-0.248,0.059C0.699,0.769,0.64,0.88,0.64,1v30	c0,0.199,0.161,0.36,0.36,0.36h30c0.199,0,0.36-0.161,0.36-0.36V1C31.36,0.904,31.322,0.813,31.255,0.746z M1.36,20.363l9.771-0.003	L1.36,30.131V20.363z M11.64,30.64H1.869l9.771-9.771C11.64,20.869,11.64,30.64,11.64,30.64z M30.64,30.64H12.36V20.15L25.64,6.87V9	h0.721V5.64H23v0.72h2.131l-13.28,13.28L1.36,19.643V1.363L30.64,1.36V30.64z"></path>
</svg>