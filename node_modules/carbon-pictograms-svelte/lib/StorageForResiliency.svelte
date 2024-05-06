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
  <path d="M31,31.36H16	c-0.199,0-0.36-0.161-0.36-0.36V19c0-0.199,0.161-0.36,0.36-0.36h15c0.199,0,0.36,0.161,0.36,0.36v12	C31.36,31.199,31.199,31.36,31,31.36z M16.36,30.64h14.28v-3.28H16.36V30.64z M16.36,26.64h14.28v-3.28H16.36V26.64z M16.36,22.64	h14.28v-3.28H16.36V22.64z M13,31.36C6.185,31.36,0.64,25.815,0.64,19V6c0-0.199,0.161-0.36,0.36-0.36	c4.354,0,8.635-1.784,11.746-4.895c0.141-0.141,0.368-0.141,0.509,0C16.365,3.856,20.646,5.64,25,5.64c0.199,0,0.36,0.161,0.36,0.36	v11h-0.72V6.356C20.339,6.263,16.134,4.511,13,1.504C9.866,4.511,5.661,6.263,1.36,6.356V19c0,6.418,5.222,11.64,11.64,11.64V31.36z M20,29.36h-2v-0.72h2V29.36z M20,25.36h-2v-0.72h2V25.36z M20,21.36h-2v-0.72h2V21.36z"></path>
</svg>