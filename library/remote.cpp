#include "lemonator_proxy.hpp"
#include "lemonator_application.hpp"

int main( void ){	
   auto hw = lemonator_proxy();
   auto app = lemonator_application( hw );
   app.run();
}