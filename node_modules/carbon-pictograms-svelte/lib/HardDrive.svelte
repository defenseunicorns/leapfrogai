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
  <path d="M26,6c-0.552,0-1-0.448-1-1s0.448-1,1-1s1,0.448,1,1S26.552,6,26,6z M27,16c0-0.552-0.448-1-1-1	s-1,0.448-1,1s0.448,1,1,1S27,16.552,27,16z M27,27c0-0.552-0.448-1-1-1s-1,0.448-1,1s0.448,1,1,1S27,27.552,27,27z M31,31.36H1	c-0.199,0-0.36-0.161-0.36-0.36v-8c0-0.199,0.161-0.36,0.36-0.36h30c0.199,0,0.36,0.161,0.36,0.36v8	C31.36,31.199,31.199,31.36,31,31.36z M1.36,30.64h29.28v-7.28H1.36V30.64z M31,20.36H1c-0.199,0-0.36-0.161-0.36-0.36v-8	c0-0.199,0.161-0.36,0.36-0.36h30c0.199,0,0.36,0.161,0.36,0.36v8C31.36,20.199,31.199,20.36,31,20.36z M1.36,19.64h29.28v-7.28	H1.36V19.64z M31,9.36H1C0.801,9.36,0.64,9.199,0.64,9V1c0-0.199,0.161-0.36,0.36-0.36h30c0.199,0,0.36,0.161,0.36,0.36v8	C31.36,9.199,31.199,9.36,31,9.36z M1.36,8.64h29.28V1.36H1.36V8.64z"></path>
</svg>