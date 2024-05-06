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
  <path d="M8,28.5c-0.552,0-1-0.448-1-1s0.448-1,1-1s1,0.448,1,1S8.552,28.5,8,28.5z M31.36,31V1	c0-0.199-0.161-0.36-0.36-0.36H7C6.801,0.64,6.64,0.801,6.64,1v5.64H1C0.801,6.64,0.64,6.801,0.64,7v24	c0,0.199,0.161,0.36,0.36,0.36h30C31.199,31.36,31.36,31.199,31.36,31z M20.36,24.36h10.28v6.279H20.36V24.36z M15.36,24.36h4.28	v6.279h-4.28C15.36,30.639,15.36,24.36,15.36,24.36z M1.36,24.36h13.28v6.279H1.36V24.36z M20.36,11c0-0.199-0.161-0.36-0.36-0.36	h-4.64V7c0-0.199-0.161-0.36-0.36-0.36H7.359V1.36h23.28v22.28H20.36V11z M15.36,11.36h4.28v12.28h-4.28	C15.36,23.64,15.36,11.36,15.36,11.36z M1.36,7.36h13.28v16.28H1.36V7.36z"></path>
</svg>