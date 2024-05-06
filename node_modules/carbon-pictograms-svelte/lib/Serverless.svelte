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
  <path d="M31,31.36h-7v-0.72h6.64V1.36H1.36V8H0.64V1	c0-0.199,0.161-0.36,0.36-0.36h30c0.199,0,0.36,0.161,0.36,0.36v30C31.36,31.199,31.199,31.36,31,31.36z M21,31.36h-5v-0.72h4.64	V11.36H1.36V16H0.64v-5c0-0.199,0.161-0.36,0.36-0.36h20c0.199,0,0.36,0.161,0.36,0.36v20C21.36,31.199,21.199,31.36,21,31.36z M13,31.36H1c-0.199,0-0.36-0.161-0.36-0.36V19c0-0.199,0.161-0.36,0.36-0.36h12c0.199,0,0.36,0.161,0.36,0.36v12	C13.36,31.199,13.199,31.36,13,31.36z M1.36,30.64h11.28V19.36H1.36V30.64z"></path>
</svg>