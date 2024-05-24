# Use
# import_gpg_key <key_name>
function import_key(){
    gpg --import $1
}
function sign_key(){
    for fingerprint in `gpg --keyid-format SHORT $1 | perl -ne 'print "$1\n" if /^\s+([A-Z0-9]+)/'`
    do
        gpg --quick-sign-key $fingerprint
    done
}
function main(){
    # import key
    import_key $1
    # sign key
    if [ -f tmp.file]; then
        rm -f tmp.file
    fi
    sign_key $1
}
main $@
