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
  <path d="M31,24.36H16c-0.199,0-0.36-0.161-0.36-0.36V12c0-0.199,0.161-0.36,0.36-0.36h15	c0.199,0,0.36,0.161,0.36,0.36v12C31.36,24.199,31.199,24.36,31,24.36z M16.36,23.64h14.28v-3.28H16.36V23.64z M16.36,19.64h14.28	v-3.28H16.36V19.64z M16.36,15.64h14.28v-3.28H16.36V15.64z M14,24.36H8c-3.99,0-7.36-3.371-7.36-7.36c0-3.99,3.37-7.36,7.36-7.36	c0.336,0,0.553,0.024,0.812,0.065C10.107,7.466,12.363,4.64,17,4.64c3.396,0,6.583,1.988,8.316,5.188l-0.633,0.343	C23.076,7.204,20.132,5.36,17,5.36c-3.405,0-5.775,1.517-7.686,4.918c-0.075,0.132-0.227,0.203-0.375,0.179	C8.576,10.395,8.376,10.36,8,10.36c-3.599,0-6.64,3.041-6.64,6.64c0,3.6,3.041,6.64,6.64,6.64h6V24.36z M20,22.36h-2v-0.72h2V22.36z M20,18.36h-2v-0.72h2V18.36z M20,14.36h-2v-0.72h2V14.36z"></path>
</svg>