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
  <path d="M5.5,16c0,0.276-0.224,0.5-0.5,0.5S4.5,16.276,4.5,16s0.224-0.5,0.5-0.5S5.5,15.724,5.5,16z M21.36,23	v-2.647c4.443-0.189,8-3.863,8-8.353V1c0-0.199-0.161-0.36-0.36-0.36h-3c-0.199,0-0.36,0.161-0.36,0.36S25.801,1.36,26,1.36h2.64V12	c0,4.213-3.427,7.64-7.64,7.64s-7.64-3.427-7.64-7.64V1.36H16c0.199,0,0.36-0.161,0.36-0.36S16.199,0.64,16,0.64h-3	c-0.199,0-0.36,0.161-0.36,0.36v11c0,4.489,3.557,8.163,8,8.353V23c0,4.213-3.427,7.64-7.64,7.64S5.36,27.213,5.36,23v-4.667	c1.131-0.174,2-1.154,2-2.333c0-1.301-1.059-2.36-2.36-2.36S2.64,14.699,2.64,16c0,1.179,0.869,2.159,2,2.333V23	c0,4.609,3.75,8.36,8.36,8.36C17.609,31.36,21.36,27.609,21.36,23z M6.64,16c0,0.904-0.736,1.64-1.64,1.64S3.36,16.904,3.36,16	S4.096,14.36,5,14.36S6.64,15.096,6.64,16z"></path>
</svg>