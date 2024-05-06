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
  <path d="M25.255,11.254l-0.51-0.509L13,22.491l-3.823-3.823	C9.29,18.47,9.36,18.244,9.36,18c0-0.75-0.61-1.36-1.36-1.36S6.64,17.25,6.64,18S7.25,19.36,8,19.36c0.244,0,0.47-0.07,0.668-0.183	L13,23.509L25.255,11.254z M8,18.64c-0.353,0-0.64-0.287-0.64-0.64S7.647,17.36,8,17.36c0.353,0,0.64,0.287,0.64,0.64	S8.353,18.64,8,18.64z M1.409,16l6.908,12.829l-0.634,0.342l-7-13c-0.058-0.107-0.058-0.235,0-0.342l7-13l0.634,0.342L1.409,16z M31.317,16.171l-7,13l-0.635-0.342L30.591,16L23.683,3.171l0.635-0.342l7,13C31.374,15.936,31.374,16.064,31.317,16.171z"></path>
</svg>