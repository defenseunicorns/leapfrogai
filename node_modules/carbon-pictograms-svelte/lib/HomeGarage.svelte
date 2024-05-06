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
  <path d="M31,31.36H1v-0.72h1.64V19h0.72v11.64h4.28V19c0-0.199,0.161-0.36,0.36-0.36h16	c0.199,0,0.36,0.161,0.36,0.36v11.64h4.279V19h0.721v11.64H31V31.36z M8.36,30.64h15.28v-3.28L8.36,27.363V30.64z M8.36,23.363	v3.279l15.28-0.002v-3.28L8.36,23.363z M8.36,19.36v3.282l15.28-0.002v-3.28H8.36z M8,16.363v-0.72l16-0.003v0.72L8,16.363z M30.745,16.254L16,1.509L1.254,16.254l-0.509-0.509l15-15c0.141-0.141,0.368-0.141,0.509,0L28.64,13.131V9h0.721v4.851l1.895,1.895	L30.745,16.254z"></path>
</svg>