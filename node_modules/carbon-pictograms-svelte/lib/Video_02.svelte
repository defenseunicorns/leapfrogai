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
  <path d="M31,31.36H1v-0.72h30V31.36z M31,24.36H1c-0.199,0-0.36-0.161-0.36-0.36V2c0-0.199,0.161-0.36,0.36-0.36	h30c0.199,0,0.36,0.161,0.36,0.36v22C31.36,24.199,31.199,24.36,31,24.36z M1.36,23.64h29.28V2.36H1.36V23.64z M12.005,18.552	c-0.062,0-0.125-0.017-0.18-0.049c-0.111-0.064-0.18-0.183-0.18-0.312V7.799c0-0.128,0.068-0.248,0.18-0.312	c0.111-0.063,0.249-0.063,0.36,0l9,5.197c0.111,0.064,0.181,0.183,0.181,0.312s-0.069,0.248-0.181,0.312l-9,5.196	C12.129,18.535,12.067,18.552,12.005,18.552z M12.365,8.422v9.145l7.92-4.572L12.365,8.422z"></path>
</svg>