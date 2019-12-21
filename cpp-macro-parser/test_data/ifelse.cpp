#ifndef MCTEST
    #ifdef MC1
        #ifdef MC2
        #else
        #endif //end MC2
    #else
        #ifdef MC2
        #else
        #endif //end MC2
    #endif //MC1
    #ifdef MC2
    #endif
#endif // !MC_TEST
