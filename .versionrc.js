const pkgUpdater = {
    VERSION_REGEX: /__version__ = "(.+)"/,

    readVersion: function (contents) {
        const version = this.VERSION_REGEX.exec(contents)[1];
        return version;
    },

    writeVersion: function (contents, version) {
        return contents.replace(this.VERSION_REGEX.exec(contents)[0], `__version__ = "${version}"`);
    }
}

module.exports = {
    bumpFiles: [{ filename: './original_metaplex_python/__pkg__.py', updater: pkgUpdater }],
}
