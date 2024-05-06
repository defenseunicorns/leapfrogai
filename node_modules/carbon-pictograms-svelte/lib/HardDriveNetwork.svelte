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
  <path d="M20,6c-0.552,0-1-0.448-1-1s0.448-1,1-1s1,0.448,1,1S20.552,6,20,6z M21,16	c0-0.552-0.448-1-1-1s-1,0.448-1,1s0.448,1,1,1S21,16.552,21,16z M21,27c0-0.552-0.448-1-1-1s-1,0.448-1,1s0.448,1,1,1	S21,27.552,21,27z M24,31.36H1c-0.199,0-0.36-0.161-0.36-0.36v-8c0-0.199,0.161-0.36,0.36-0.36h23c0.199,0,0.36,0.161,0.36,0.36v8	C24.36,31.199,24.199,31.36,24,31.36z M1.36,30.64h22.28v-7.28H1.36V30.64z M31,27.36h-5v-0.72h4.64V16.36H26v-0.72h4.64V5.36H26	V4.64h5c0.199,0,0.36,0.161,0.36,0.36v22C31.36,27.199,31.199,27.36,31,27.36z M24,20.36H1c-0.199,0-0.36-0.161-0.36-0.36v-8	c0-0.199,0.161-0.36,0.36-0.36h23c0.199,0,0.36,0.161,0.36,0.36v8C24.36,20.199,24.199,20.36,24,20.36z M1.36,19.64h22.28v-7.28	H1.36V19.64z M24,9.36H1C0.801,9.36,0.64,9.199,0.64,9V1c0-0.199,0.161-0.36,0.36-0.36h23c0.199,0,0.36,0.161,0.36,0.36v8	C24.36,9.199,24.199,9.36,24,9.36z M1.36,8.64h22.28V1.36H1.36V8.64z"></path>
</svg>