module.exports = function (api) {
    const presets = [
        // ['@babel/preset-env', {targets: {node: true}, modules: 'auto'}],
        ['@babel/preset-react', {runtime: 'automatic'}],
        // '@babel/preset-env',
        // '@babel/preset-react',
        ['@babel/preset-env', {targets: {node: 'current'}}],
    ];
    const plugins = [
        '@babel/plugin-transform-runtime',
    ];

    /** this is just for minimal working purposes,
     * for testing larger applications it is
     * advisable to cache the transpiled modules in
     * node_modules/.bin/.cache/@babel/register* */
    api.cache(false);

    return {
        presets,
        plugins
    };
};