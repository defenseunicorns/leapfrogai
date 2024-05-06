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
  <path d="M31.36,0.64V10h-0.72V1.87L19.255,13.254l-0.51-0.509	L30.131,1.36H22V0.64H31.36z M28.64,22.64H9.36V3.36H18V2.64H9C8.801,2.64,8.64,2.801,8.64,3v20c0,0.199,0.161,0.36,0.36,0.36h20	c0.199,0,0.36-0.161,0.36-0.36v-9h-0.72V22.64z M12.64,30.64H1.36V19.36H7v-0.72H1c-0.199,0-0.36,0.161-0.36,0.36v12	c0,0.199,0.161,0.36,0.36,0.36h12c0.199,0,0.36-0.161,0.36-0.36v-6h-0.72C12.64,25,12.64,30.64,12.64,30.64z"></path>
</svg>